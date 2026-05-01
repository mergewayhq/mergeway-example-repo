"""Generated Mergeway entity models."""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any, ClassVar
from mergeway.models import GeneratedModel

@dataclass(slots=True)
class Comment(GeneratedModel):
    __mergeway_entity_name__: ClassVar[str] = 'Comment'
    __mergeway_field_aliases__: ClassVar[dict[str, str]] = {}
    id: str
    post: str
    author: str
    content: str
    created_at: str

@dataclass(slots=True)
class Post(GeneratedModel):
    __mergeway_entity_name__: ClassVar[str] = 'Post'
    __mergeway_field_aliases__: ClassVar[dict[str, str]] = {}
    id: str
    title: str
    author: str
    tags: list[str] | None = None
    body: str | None = None

@dataclass(slots=True)
class Tag(GeneratedModel):
    __mergeway_entity_name__: ClassVar[str] = 'Tag'
    __mergeway_field_aliases__: ClassVar[dict[str, str]] = {}
    id: str
    label: str

@dataclass(slots=True)
class User(GeneratedModel):
    __mergeway_entity_name__: ClassVar[str] = 'User'
    __mergeway_field_aliases__: ClassVar[dict[str, str]] = {}
    id: str
    name: str
    email: str
    roles: list[str] | None = None

ENTITY_REGISTRY = {
    'Comment': Comment,
    'Post': Post,
    'Tag': Tag,
    'User': User,
}

__all__ = ['Comment', 'Post', 'Tag', 'User', 'ENTITY_REGISTRY']
