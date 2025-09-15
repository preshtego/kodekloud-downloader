import logging
import click
from pathlib import Path

from kodekloud_downloader.main import (
    parse_course_from_url,
    download_course,
    download_quiz,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.group()
def kodekloud():
    """KodeKloud Downloader CLI"""
    pass


@kodekloud.command()
@click.argument("url")
@click.option("--token", required=True, help="Bearer token from DevTools")
@click.option("--quality", default="720p", help="Video quality (default: 720p)")
@click.option("--output-dir", default="./downloads", help="Directory to save course")
@click.option("--max-duplicate-count", default=3, help="Max retries before token is considered expired")
def dl(url, token, quality, output_dir, max_duplicate_count):
    """
    Download a course from KodeKloud.

    URL: course page link (e.g. https://learn.kodekloud.com/course/docker-for-the-absolute-beginner)
    """
    logger.info(f"Fetching course from {url}...")
    course = parse_course_from_url(url)

    download_course(
        course=course,
        token=token,
        quality=quality,
        output_dir=Path(output_dir),
        max_duplicate_count=max_duplicate_count,
    )


@kodekloud.command()
@click.option("--output-dir", default="./downloads/quizzes", help="Directory to save quizzes")
@click.option("--sep", is_flag=True, help="Save each quiz separately")
def quizzes(output_dir, sep):
    """Download all KodeKloud quizzes as Markdown."""
    download_quiz(output_dir, sep)


if __name__ == "__main__":
    kodekloud()
