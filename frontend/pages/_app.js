import Layout from '../src/components/Layout';
import AuthContext from '../src/components/context/AuthContext';
import NProgress from '../src/components/common/ProgressIndicator';
import '../src/styles/index.css';
import '../src/styles/basecss.css';
import '../src/styles/nprogress.css';

function MyApp({ Component, pageProps }) {
  return (
    <AuthContext>
      <NProgress />
      <Layout>
        <Component {...pageProps} />
      </Layout>
    </AuthContext>
  );
}

export default MyApp;
