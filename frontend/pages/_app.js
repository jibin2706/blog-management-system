import Layout from '../src/components/Layout';
import AuthContext from '../src/components/context/AuthContext';
import '../src/styles/index.css';
import '../src/styles/basecss.css';

function MyApp({ Component, pageProps }) {
  return (
    <AuthContext>
      <Layout>
        <Component {...pageProps} />
      </Layout>
    </AuthContext>
  );
}

export default MyApp;
