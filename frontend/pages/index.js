import React from 'react';
import axios from '../src/utils/axios';
import clsx from 'clsx';
import ArticleCard from '../src/components/common/ArticleCard';
import css from '../src/styles/pages/index.module.css';

function index({ featuredPosts, latestPosts }) {
  return (
    <main style={{ maxWidth: '800px', margin: 'auto', padding: '0 1rem' }}>
      <section className="mt4">
        <div className="center">
          <h2 className={clsx(css.sectionHeader)}>Featured Posts</h2>
        </div>
        <div className={css.postListContainer}>
          {featuredPosts.map((post) => (
            <ArticleCard key={post.id} {...post} />
          ))}
        </div>
      </section>
      <section className="mt4">
        <div className="center">
          <h2 className={clsx(css.sectionHeader)}>Latest Posts</h2>
        </div>
        <div className={css.postListContainer}>
          {latestPosts.map((post) => (
            <ArticleCard key={post.id} {...post} />
          ))}
        </div>
      </section>
    </main>
  );
}

export async function getServerSideProps() {
  const featuredPosts = axios.get('/posts?type=featured').then((response) => {
    return response.data.posts;
  });

  const latestPosts = axios.get('/posts?type=latest').then((response) => {
    return response.data.posts;
  });

  return {
    props: {
      featuredPosts: await featuredPosts,
      latestPosts: await latestPosts,
    },
  };
}

export default index;
