from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
# Database
from .models import Video


class TestHomePageMessage(TestCase):
    def test_app_title_message_shown_on_home_page(self):
        url = reverse('home')  # Url to home page
        # Make a request to the home page from the client side. The value for the response will be the status code: e.g( <HttpResponse status_code=200, "text/html; charset=utf-8">)
        response = self.client.get(url)
        print('Status Code: ', response)

        self.assertContains(response, "The Weeknd")

    # Testing adding video to video list

    def test_add_video(self):

        # Example data of a YT video data input
        valid_video = {
            'name': "“I Was Never There” by The Weeknd but heartbroken in your loft.",
            'url': 'https://www.youtube.com/watch?v=wtlN-eNmjzI',
            'notes': 'This will be me soon in the future...'
        }

        # Make a POST request to add video
        # Note: If the post request was successful, it will send back a 200 status code. However, in our original code, we are redirecting, which will give us the status code 302. The tests doesn't know that, so we need to give the response to follow that redirection
        url = reverse('add_video')
        response = self.client.post(url, data=valid_video, follow=True)

        print(f'Response POST Status: {response}')

        # Assert template is used after the POST request was made, as in the original function in views.add, we are redirecting to the video_list.html
        self.assertTemplateUsed('video_collection/video_list.html')

        # In the video list that was redirected, is the video that we added through the POST method, does the video_list contains that video?

        # Video Title Name
        self.assertContains(
            response, "“I Was Never There” by The Weeknd but heartbroken in your loft.")

        # Video Url
        self.assertContains(
            response, 'https://www.youtube.com/watch?v=wtlN-eNmjzI')

        # Video Notes
        self.assertContains(response, 'This will be me soon in the future...')

        # Check the django's db to see if the video contains this?
        video_count = Video.objects.count()

        # Check to see of there is 1 video object in the db
        self.assertEqual(1, video_count)

        video = Video.objects.first()  # Getting the First object from the db

        # Check if the video name from the db is same as the testing value name
        self.assertEqual(
            '“I Was Never There” by The Weeknd but heartbroken in your loft.', video.name)

        # Video URL
        self.assertEqual(
            'https://www.youtube.com/watch?v=wtlN-eNmjzI', video.url)

        # Notes
        self.assertEqual('This will be me soon in the future...', video.notes)

        # Video ID
        self.assertEqual('wtlN-eNmjzI', video.video_id)

    def test_invalid_video_url_added(self):
        # List of invalid urls
        invalid_video_urls = [
            'https://www.youtube.com/watch',  'https://www.youtube.com/watch?', 'https://www.youtube.com/watch?abc=1234', 'https://www.youtube.com/watch?v=',
            'https://github.com',
            'https://minneapolis.edu',
            'https://minneapolis.edu?v=fdfads343'
        ]

        for invalid_video_url in invalid_video_urls:
            new_video = {
                'name': 'example',
                'url': invalid_video_url,
                'notes': 'example notes'
            }

            url = reverse('add_video')  # Url will be the add video site

            # Adding invalid new video
            response = self.client.post(url, data=new_video)

            # Assert that the template was used
            self.assertTemplateUsed('video_collection/add.html')

            # The messages that was being used to display mini messages for warning, info, etc
            messages = response.context['messages']

            # Extract that messages' message
            message_text = [message.message for message in messages]

            # Look for a string inside a list of strings
            self.assertIn('Invalid Youtube URL', message_text)
            self.assertIn('Please check data entered.', message_text)

            video_count = Video.objects.count()  # Should be 0

            # Assert that the video_count from the db is 0
            self.assertEqual(0, video_count)


class TestVideoList(TestCase):
    def test_all_videos_displayed_in_correct_order(self):
        # these 4 dummy videos will be created and save to the db
        v1 = Video.objects.create(
            name='abc', notes='example', url='https://www.youtube.com/watch?v=123')
        v2 = Video.objects.create(
            name='AAA', notes='example', url='https://www.youtube.com/watch?v=124')
        v3 = Video.objects.create(
            name='xcc', notes='example', url='https://www.youtube.com/watch?v=125')
        v4 = Video.objects.create(
            name='lmn', notes='example', url='https://www.youtube.com/watch?v=126')

        expected_list_order = [v2, v1, v4, v3]

        url = reverse('video_list')
        response = self.client.get(url)

        # The context is all the data combined that goes with 'video_list' template when users make a request to that page. For example,the dictionary of users data, the html page rendering,video objects values ,styles, the search form, etc
        # Look up the videos from the dictionary key
        # Need to convert to python list as the videos_in_template sends in <QuerySet ...> tag instead of a list, else this will cause the assertEqual method to return false e.g(AssertionError: <QuerySet [<Video: ID: 2, Name: AAA, URL:[365 chars]le>]> != [<Video: ID: 2, Name: AAA, URL: https://w[354 chars]ple>])
        videos_in_template = list(response.context['videos'])

        # Expect the videos in template to be equal to the expected list order
        self.assertEqual(videos_in_template, expected_list_order)

    # Check no videos are shown, since the dummy videos are invalid for testing purpose
    def test_no_video_message(self):
        url = reverse('video_list')
        response = self.client.get(url)

        # Make sure it doesn't contains the 'No Videos Found!' message from the messages library that was suppose to display to users html
        self.assertContains(response, 'No Videos Found!')

        # The video list should be 0
        self.assertEqual(0, len(response.context['videos']))

    # Checking if the '1 video' message does display to users when 1 video is added to the video list

    def test_video_number_message_one_video(self):
        v1 = Video.objects.create(
            name='abc', notes='example', url='https://www.youtube.com/watch?v=123')

        # Req to the video_list html
        # Make a get req
        url = reverse('video_list')
        response = self.client.get(url)

        # Checking to see and assert that the response contains the '1 Video' message
        self.assertContains(response, '1 Video')

        # Also check the response does NOT contain Videos (plural)s
        self.assertNotContains(response, '1 Videos')

    # Checking if '2 Videos' message is displayed
    def test_video_number_message_two_videos(self):
        v1 = Video.objects.create(
            name='abc', notes='example', url='https://www.youtube.com/watch?v=123')
        v2 = Video.objects.create(
            name='AAA', notes='example', url='https://www.youtube.com/watch?v=124')

        url = reverse('video_list')
        response = self.client.get(url)

        # Checking to see and assert that the response from url contains the '2 Videos' message
        self.assertContains(response, '2 Videos')


class TestVideoSearch(TestCase):
    # Similar to your GH repo tests

    def test_video_search_matches(self):
        # these 4 dummy videos will be created and save to the db
        v1 = Video.objects.create(
            name='abc', notes='example', url='https://www.youtube.com/watch?v=123')
        v2 = Video.objects.create(
            name='ABC', notes='example', url='https://www.youtube.com/watch?v=124')
        v3 = Video.objects.create(
            name='xcc', notes='example', url='https://www.youtube.com/watch?v=125')
        v4 = Video.objects.create(
            name='lmn', notes='example', url='https://www.youtube.com/watch?v=126')

        # v1 will appear first when searched 'ABC'
        expected_list_order = [v1, v2]

        # Mimicking a get request to the video_list WITH the parameter search term of one of the video name
        # e.g(video_list?search_term=weeknd)
        response = self.client.get(reverse('video_list') + '?search_term=ABC')

        videos_in_template = list(response.context['videos'])

        self.assertEqual(expected_list_order, videos_in_template)

    # No search matches keyword
    def test_video_no_match(self):
        # these 4 dummy videos will be created and save to the db
        v1 = Video.objects.create(
            name='abc', notes='example', url='https://www.youtube.com/watch?v=123')
        v2 = Video.objects.create(
            name='ABC', notes='example', url='https://www.youtube.com/watch?v=124')
        v3 = Video.objects.create(
            name='xcc', notes='example', url='https://www.youtube.com/watch?v=125')
        v4 = Video.objects.create(
            name='lmn', notes='example', url='https://www.youtube.com/watch?v=126')

        # No search order will appear for non existent search word
        expected_list_order = []

        # Mimicking a get request to the video_list WITH the parameter search term of one of the video name
        # e.g(video_list?search_term=weeknd)
        response = self.client.get(
            reverse('video_list') + '?search_term=HELLO')

        videos_in_template = list(response.context['videos'])

        self.assertEqual(expected_list_order, videos_in_template)

        # The response should be no videos when users search for 'hello'
        self.assertContains(response, 'No Videos Found!')

        # Check if the message says '0 Videos' on video_list HTML
        self.assertContains(response, '0 Videos')


class TestVideoModel(TestCase):
    # Invalid url should raise validation error
    def test_invalid_url_raise_validation_error(self):
        # List of invalid urls, with more examples
        invalid_video_urls = [
            'https://www.youtube.com/watch',  'https://www.youtube.com/watch?', 'https://www.youtube.com/watch?abc=1234', 'https://www.youtube.com/watch?v=',
            'https://github.com',
            'https://minneapolis.edu',
            'https://minneapolis.edu?v=fdfads343',
            'https://www.youtube.com/watch/something'
            'https://www.youtube.com/watch/something?v=12132kjk',
            'hhhhffdhttps://www.youtube.com/watch/something?v=12132kjk',
            'hhhhffdhttps:////www.youtube.com/watch/something?v=12132kjk',
            'https://wwww.youtube.com/watch/something?v=12132kjk',
            'https://www.youtube..com/watch/something?v=12132kjk',
            'https://www.youtube..com/watch//something?v=12132kjk',
            'https://www.youtube..com/watch/something?v=12132kjk/watch/?v=SWzAQXDYjMY',
            'https:///www.youtube.com/watch/?v=SWzAQXDYjMY',
            'http://www.youtube.com/watch/?v=SWzAQXDYjMY',
        ]

        for invalid_YT_url in invalid_video_urls:
            with self.assertRaises(ValidationError):
                Video.objects.create(name='example',
                                     url=invalid_YT_url,
                                     notes='Example Note',)

        self.assertEqual(0, Video.objects.count())

    # duplicate videos raises integrity error
    def test_duplicate_video_raises_integrity_error(self):
        v1 = Video.objects.create(
            name='abc', notes='example', url='https://www.youtube.com/watch?v=123')

        with self.assertRaises(IntegrityError):
            # Adding duplicate video to raise integrity error
            Video.objects.create(
                name='abc', notes='example', url='https://www.youtube.com/watch?v=123')
