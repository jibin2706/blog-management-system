import React, { useState, useContext, useEffect } from 'react';
import { useRouter } from 'next/router';
import clsx from 'clsx';
import axios from '../src/utils/axios';
import { AuthContext } from '../src/components/context/AuthContext';
import css from '../src/styles/pages/write.module.css';

function write({ detail }) {
  const post = detail.post;
  const writer = detail.writer;

  const router = useRouter();
  // page can be of 2 types -> 1. add new post  2. update existing post
  // change this state by using query param
  // when update=1 change state to 'UPDATE'
  const [type, setType] = useState('ADD');
  const { authenticated, userInfo, token } = useContext(AuthContext);
  const [formData, setFormData] = useState({
    title: 'test',
    url_slug: '',
    body: '',
    is_publish: false,
  });

  useEffect(() => {
    if (!authenticated) router.push('/login');
  }, [authenticated]);

  useEffect(() => {
    if (router.query.update === '1') {
      setType('UPDATE');
    }
  }, [router]);

  useEffect(() => {
    if (writer.email === userInfo.email) {
      setFormData({
        title: post.title,
        url_slug: post.url_slug,
        body: post.body,
        is_publish: post.is_publish,
      });
    }
  }, [post]);

  const handleInputChange = (e) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;

    setFormData({
      ...formData,
      [e.target.name]: value,
    });
  };

  const submitPost = (e) => {
    e.preventDefault();
    let method = 'POST';
    let data = formData;
    if (type === 'UPDATE') {
      data.id = post.id;
      method = 'PATCH';
    }

    axios({
      method,
      url: '/post',
      data: data,
      headers: {
        Authorization: token,
      },
    })
      .then((response) => {
        const data = response.data;
        router.push('/');
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return (
    <div className={clsx(css.container)}>
      <form onSubmit={submitPost}>
        <label className={clsx(css.label)}>
          <span>Post Title</span>
          <input type="text" name="title" onChange={handleInputChange} value={formData.title} required />
        </label>
        <label className={clsx(css.label)}>
          <span>Post url (Unique link for your post)</span>
          <input type="text" name="url_slug" onChange={handleInputChange} value={formData.url_slug} required />
        </label>
        <label className={clsx(css.label)}>
          <span>
            Body <small>In Markdown</small>
          </span>
          <textarea name="body" onChange={handleInputChange} value={formData.body} rows="5" cols="50" required />
        </label>
        <label className={clsx(css.label)}>
          <span>Publish</span>
          <input type="checkbox" name="is_publish" onChange={handleInputChange} checked={formData.is_publish} />
        </label>

        {type === 'ADD' ? (
          <button>{formData.is_publish ? 'Publish Post' : 'Save Draft'}</button>
        ) : (
          <button>Update Post</button>
        )}
      </form>
    </div>
  );
}

export async function getServerSideProps({ query }) {
  const url_slug = query.postUrl;
  if (url_slug) {
    const post = axios(`/post?url=${url_slug}`).then((response) => {
      return response.data;
    });

    return {
      props: {
        detail: await post,
      },
    };
  }

  return {
    props: {},
  };
}

export default write;
