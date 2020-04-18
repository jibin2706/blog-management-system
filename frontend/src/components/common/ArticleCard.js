import React from 'react';
import PropTypes from 'prop-types';
import Link from 'next/link';
import css from './ArticleCard.module.css';

function ArticleCard({ title, body, created_at, url_slug }) {
  return (
    <Link href="/post/[title]" as={`/post/${url_slug}`}>
      <a className={css.card}>
        <section>
          <h3 className={css.title}>{title}</h3>
          <p className={css.date}>{created_at}</p>
          <p className={css.body}>{body}</p>
          <span className={css.more}>Read more</span>
        </section>
      </a>
    </Link>
  );
}

ArticleCard.propTypes = {
  body: PropTypes.string.isRequired,
  created_at: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  url_slug: PropTypes.string.isRequired,
};

export default ArticleCard;
