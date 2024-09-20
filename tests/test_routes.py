import pytest
from app import app, get_db_connection

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    # Setup: Create tables before running tests
    with app.app_context():
        conn = get_db_connection()
        conn.execute('DROP TABLE IF EXISTS posts')
        conn.execute(''' 
            CREATE TABLE posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL
            )
        ''')
        conn.commit()

    yield client

    # Teardown: Close the connection after the test
    conn.close()

def test_index(client):
    """Test if index page is loading correctly."""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'No posts yet' in rv.data

def test_create_post(client):
    """Test the creation of a new post."""
    rv = client.post('/create', data={'title': 'Test Post', 'content': 'Test Content'}, follow_redirects=True)
    assert rv.status_code == 200
    assert b'Test Post' in rv.data

def test_edit_post(client):
    """Test editing an existing post."""
    # First, create a post to edit
    client.post('/create', data={'title': 'Original Title', 'content': 'Original Content'}, follow_redirects=True)
    
    # Retrieve the post ID (assuming ID is 1 for simplicity)
    conn = get_db_connection()
    post_id = conn.execute('SELECT id FROM posts WHERE title = ?', ('Original Title',)).fetchone()['id']
    conn.close()

    # Edit the post
    rv = client.post(f'/{post_id}/edit', data={'title': 'Updated Title', 'content': 'Updated Content'}, follow_redirects=True)
    assert rv.status_code == 200
    assert b'Updated Title' in rv.data

def test_delete_post(client):
    """Test deleting an existing post."""
    # First, create a post to delete
    client.post('/create', data={'title': 'Post to Delete', 'content': 'Delete this post'}, follow_redirects=True)
    
    # Retrieve the post ID (assuming ID is 1 for simplicity)
    conn = get_db_connection()
    post_id = conn.execute('SELECT id FROM posts WHERE title = ?', ('Post to Delete',)).fetchone()['id']
    conn.close()

    # Delete the post
    rv = client.post(f'/{post_id}/delete', follow_redirects=True)
    assert rv.status_code == 200
    assert b'was successfully deleted!' in rv.data

    # Verify the post no longer exists
    rv = client.get('/')
    assert b'Post to Delete' not in rv.data
