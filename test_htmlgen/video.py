from unittest import TestCase

from asserts import assert_equal, assert_true, assert_is_none, assert_false

from htmlgen import Video, Preload


class VideoTest(TestCase):
    def test_src_only(self):
        video = Video("foo.mp4")
        assert_equal(
            [b'<video src="foo.mp4">', b"</video>"], list(iter(video)),
        )

    def test_controls(self):
        video = Video("foo.mp4")
        assert_false(video.controls)
        video.controls = True
        assert_true(video.controls)
        assert_equal(
            [b'<video controls="controls" src="foo.mp4">', b"</video>"],
            list(iter(video)),
        )

    def test_poster(self):
        video = Video("foo.mp4")
        assert_is_none(video.poster)
        video.poster = "poster.png"
        assert_equal("poster.png", video.poster)
        assert_equal(
            [b'<video poster="poster.png" src="foo.mp4">', b"</video>"],
            list(iter(video)),
        )

    def test_preload(self):
        video = Video("foo.mp4")
        assert_is_none(video.preload)
        video.preload = Preload.NONE
        assert_equal(
            [b'<video preload="none" src="foo.mp4">', b"</video>"],
            list(iter(video)),
        )
