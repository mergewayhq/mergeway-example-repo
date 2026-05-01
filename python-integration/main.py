from __future__ import annotations

import shutil
import sys
import tempfile
from collections import Counter
from mergeway import Database
from pathlib import Path


INTEGRATION_ROOT = Path(__file__).resolve().parent
REPO_ROOT = INTEGRATION_ROOT.parent


def heading(title: str) -> None:
    print(f"\n=== {title} ===")


def print_lines(lines: list[str]) -> None:
    for line in lines:
        print(line)


def summarize_repository(db: Database) -> None:
    heading("Current Repository Snapshot")

    entities = db.list_entities()
    print(f"Entities: {', '.join(entities)}")

    users = db.export("User")
    posts = db.export("Post")
    comments = db.export("Comment")
    tags = db.export("Tag")

    print(f"Users: {len(users)}")
    print(f"Posts: {len(posts)}")
    print(f"Comments: {len(comments)}")
    print(f"Tags: {len(tags)}")

    author_lookup = {user.id: user.name for user in users}
    tag_lookup = {tag.id: tag.label for tag in tags}
    comments_by_post = Counter(comment.post for comment in comments)

    print_lines(
        [
            (
                f"- {post.title} by {author_lookup.get(post.author, post.author)} "
                f"[tags: {', '.join(tag_lookup.get(tag, tag) for tag in post.tags)}] "
                f"has {comments_by_post.get(post.id, 0)} comment(s)"
            )
            for post in posts
        ]
    )


def run_launch_retro_workflow(db: Database) -> None:
    heading("Launch Retrospective Workflow")

    User = db.classes_module.User
    Tag = db.classes_module.Tag
    Post = db.classes_module.Post
    Comment = db.classes_module.Comment

    created_user = db.create(
        User,
        User(
            id="user-cara",
            name="Cara Community",
            email="cara@example.com",
            roles=["author"],
        ),
    )
    print(f"Created author: {created_user.name} ({created_user.id})")

    promoted_user = db.update(
        "User",
        "user-cara",
        {"roles": ["author", "editor"]},
        merge=True,
    )
    print(f"Expanded roles: {', '.join(promoted_user.roles)}")

    created_tag = db.create(
        Tag,
        Tag(
            id="tag-community",
            label="Community Stories",
        ),
    )
    print(f"Created tag: {created_tag.label}")

    created_post = db.create(
        Post,
        Post(
            id="post-002",
            title="What We Learned From Launch Day",
            author="user-cara",
            tags=["tag-product", "tag-community"],
            body=(
                "Launch week surfaced the strongest customer stories, the fastest "
                "editorial feedback loops, and a clear follow-up theme for the blog."
            ),
        ),
    )
    print(f"Created post: {created_post.title}")

    created_comment = db.create(
        Comment,
        Comment(
            id="comment-002",
            post="post-002",
            author="user-bob",
            content="Let's turn the launch recap into a recurring customer update series.",
            created_at="2026-05-01T10:30:00Z",
        ),
    )
    print(f"Created comment: {created_comment.id}")

    validation_result = db.validate()
    print(f"Validation: {validation_result}")

    format_result = db.format(in_place=True).strip()
    print("Format result:")
    print(format_result or "(no files changed)")

    export_snapshot = db.export()
    post_titles = [post.title for post in export_snapshot["Post"]]
    comment_counts = Counter(comment.post for comment in export_snapshot["Comment"])

    print_lines(
        [
            "Repository now contains:",
            f"- {len(export_snapshot['User'])} users",
            f"- {len(export_snapshot['Tag'])} tags",
            f"- {len(export_snapshot['Post'])} posts",
            f"- {len(export_snapshot['Comment'])} comments",
            f"- Post titles: {', '.join(post_titles)}",
            f"- New post discussion count: {comment_counts.get('post-002', 0)}",
        ]
    )

    heading("Cleanup")
    print(db.delete("Comment", "comment-002"))
    print(db.delete("Post", "post-002"))
    print(db.delete("Tag", "tag-community"))
    print(db.delete("User", "user-cara"))
    print(f"Post-cleanup validation: {db.validate()}")


def build_temporary_workspace() -> Path:
    tempdir = Path(tempfile.mkdtemp(prefix="mergeway-integration-"))
    workspace = tempdir / REPO_ROOT.name
    shutil.copytree(
        REPO_ROOT,
        workspace,
        ignore=shutil.ignore_patterns(".git", ".venv", "__pycache__", ".pytest_cache"),
    )
    return workspace


def main() -> None:
    heading("Mergeway Python Example")
    print(f"Source repository: {REPO_ROOT}")
    print("Use-case: rehearse a launch retrospective workflow without touching the real repo.")

    #workspace = build_temporary_workspace()
    #print(f"Working copy: {workspace}")

    db = Database(REPO_ROOT / "mergeway.yaml")
    generated_models = db.generate_classes(INTEGRATION_ROOT / "generated_models.py")
    print(f"Generated typed models at: {generated_models.relative_to(REPO_ROOT)}")

    summarize_repository(db)
    run_launch_retro_workflow(db)

    heading("Done")


if __name__ == "__main__":
    main()
