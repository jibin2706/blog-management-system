import React from 'react';
import clsx from 'clsx';
import axios from '../../src/utils/axios';
import css from '../../src/styles/pages/postdetail.module.css';

function PostDetail({ detail }) {
  const post = detail.post;
  const writer = detail.writer;

  return (
    <article style={{ maxWidth: '800px', margin: 'auto', padding: '0 1rem' }}>
      <header>
        <h1 className={clsx(css.title)}>{post.title}</h1>
        <p>{post.created_at}</p>
        <p className={css.authorHeader}>
          <img className={clsx(css.avatar)} src={writer.picture} alt="Author's profile photo" />
          {writer.name}
        </p>
      </header>
      <main className={clsx(css.body)}>
        <p>{post.body}</p>
      </main>

      {writer.bio && (
        <section className={css.authorInfo}>
          <h3>About Author</h3>
          <p>{writer.bio}</p>
        </section>
      )}
    </article>
  );
}

export async function getServerSideProps(context) {
  // getting url params from context object
  const url_slug = context.params.title;

  const post = axios.get(`/post?url=${url_slug}`).then((response) => {
    console.log(response);
    return response.data;
  });

  return {
    props: {
      detail: await post,
    },
  };
}

export default PostDetail;
