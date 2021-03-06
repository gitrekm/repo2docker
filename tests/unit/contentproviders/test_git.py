import os
import pytest
from tempfile import TemporaryDirectory
from repo2docker.contentproviders import Git


def test_clone(repo_with_content):
    """Test simple git clone to a target dir"""
    upstream, sha1 = repo_with_content

    with TemporaryDirectory() as clone_dir:
        spec = {'repo': upstream}
        git_content = Git()
        for _ in git_content.fetch(spec, clone_dir):
            pass
        assert os.path.exists(os.path.join(clone_dir, 'test'))

        assert git_content.content_id == sha1[:7]


def test_bad_ref(repo_with_content):
    """
    Test trying to checkout a ref that doesn't exist
    """
    upstream, sha1 = repo_with_content
    with TemporaryDirectory() as clone_dir:
        spec = {'repo': upstream, 'ref': 'does-not-exist'}
        with pytest.raises(ValueError):
            for _ in Git().fetch(spec, clone_dir):
                pass


def test_always_accept():
    # The git content provider should always accept a spec
    assert Git().detect('/tmp/doesnt-exist', ref='1234')
    assert Git().detect('/tmp/doesnt-exist')
    # a path that exists
    assert Git().detect('/etc', ref='1234')
    # a remote URL
    assert Git().detect('https://example.com/path/here')
