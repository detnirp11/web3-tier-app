import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import './App.css';

// バリデーションスキーマ
const schema = yup.object().shape({
  name: yup.string().required('名前は必須です'),
  email: yup
    .string()
    .email('メールアドレスの形式が正しくありません')
    .required('メールは必須です'),
});

function App() {
  const [response, setResponse] = useState(null);

  // useFormでフォームとバリデーションをセットアップ
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: yupResolver(schema),
  });

  // submit処理
  const onSubmit = async (data) => {
    try {
      const res = await fetch('http://localhost:5000/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      const result = await res.json();
      setResponse(result);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h1>ユーザー情報を送信</h1>
      <form onSubmit={handleSubmit(onSubmit)}>
        <div>
          <label>名前: </label>
          <input type="text" {...register('name')} />
          {errors.name && <p style={{ color: 'red' }}>{errors.name.message}</p>}
        </div>
        <div>
          <label>メール: </label>
          <input type="email" {...register('email')} />
          {errors.email && <p style={{ color: 'red' }}>{errors.email.message}</p>}
        </div>
        <button type="submit">送信</button>
      </form>

      {response && (
        <div style={{ marginTop: '2rem' }}>
          <h2>サーバーからの応答:</h2>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;

