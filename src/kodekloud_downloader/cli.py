@kodekloud.command()
@click.argument("course_url", required=False)
@click.option(
    "--quality",
    "-q",
    default="1080p",
    type=click.Choice([quality.value for quality in Quality]),
    help="Quality of the video to be downloaded.",
)
@click.option(
    "--output-dir",
    "-o",
    default=Path.home() / "Downloads",
    help="Output directory where downloaded files will be stored.",
)
@click.option(
    "--token",
    "-t",
    required=True,
    help="Bearer token. Copy from DevTools → Network tab → any `api/lessons` request → Headers → Authorization.",
)
@click.option(
    "--max-duplicate-count",
    "-mdc",
    default=3,
    type=int,
    help="If same video is downloaded this many times, then download stops",
)
def dl(
    course_url,
    quality: str,
    output_dir: Union[Path, str],
    token,
    max_duplicate_count: int,
):
    if course_url is None:
        courses = collect_all_courses()
        selected_courses = select_courses(courses)
        for selected_course in selected_courses:
            download_course(
                course=selected_course,
                token=token,  # 🔄 changed from cookie
                quality=quality,
                output_dir=output_dir,
                max_duplicate_count=max_duplicate_count,
            )
    elif validators.url(course_url):
        course_detail = parse_course_from_url(course_url)
        download_course(
            course=course_detail,
            token=token,  # 🔄 changed from cookie
            quality=quality,
            output_dir=output_dir,
            max_duplicate_count=max_duplicate_count,
        )
    else:
        logging.error("Please enter a valid URL")
        SystemExit(1)
