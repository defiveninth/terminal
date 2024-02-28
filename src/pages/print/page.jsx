import axios from 'axios'
import { File, Folder, Usb } from 'lucide-react'
import React, { useEffect, useState } from 'react'
import Header from '../components/Header/Header'
import DocumentModal from '../components/Modal/Modal'

const PrintPage = () => {
  const [data, setData] = useState([]);
  const [documentURL, setDocumentURL] = useState('');
  const [error, setError] = useState(false);
  const [fetch, setFetch] = useState({
    folders: '',
    type: 'devices',
  });
  const [isModalOpen, setIsModalOpen] = useState(false);

  const openModal = (filename) => {
    setIsModalOpen(true);
    fetchUrl(filename);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  const fetchData = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:1234/devices');
      if (res.data.status === 'error') setError(true);
      else {
        setError(false);
        setData(res.data);
      }
    } catch (e) {
      setError(true);
    }
  };

  const fetchUrl = async (filename) => {
    try {
      const res = await axios.get(`http://127.0.0.1:1234/devices/geturl/${filename}`);
      if (res.data.status === 'success') {
        setDocumentURL("http://127.0.0.1:1234/devices/file");
      }
    } catch (e) {
      setError(true);
    }
  };

  const fetchBack = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:1234/devices/back');
      if (res.data.status === 'error') {
        setError(true);
      } else {
        setError(false);
        setData({ ...res.data, path: res.data.path });
        if (res.data.path === '/Volumes') {
          setFetch({ ...fetch, type: 'devices' });
        }
      }
    } catch (e) {
      setError(true);
    }
  };

  const setPath = async (type, folderName) => {
    setFetch((prev) => ({ ...prev, type: type, folders: folderName }));
    if (type === 'folders') {
      try {
        const res = await axios.get(
          `http://127.0.0.1:1234/devices/folder${folderName.startsWith('/') ? '' : '/'}${folderName}`
        );
        if (res.data.status === 'error') setError(true);
        else {
          setError(false);
          setData(res.data);
        }
      } catch (e) {
        setError(true);
      }
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <>
    <div className="container mx-auto mt-20">
      <Header />
      {error ? (
        <div className=' mx-auto flex items-center justify-center flex-col mt-20'>
          <h1 className='text-2xl text-cyan-950'>USB QÙRYLGUSY TABYLMADY</h1>
          <button
            className='text-2xl px-4 py-2 bg-red-500 text-white rounded-md'
            onClick={() => fetchData()}
          >
            JANARTU
          </button>
        </div>
      ) : (
        <>
          <div className=' mx-auto'>
            <h1 className='text-2xl text-cyan-950'>USB QÙRYLGYLARY:</h1>
          </div>
          <div className=' mx-auto flex flex-wrap gap-4 p-5'>
            {data.type === 'devices' &&
              data.devices.length > 0 &&
              data.devices.map((D) => (
                <div
                  key={D}
                  className={
                    'flex flex-col items-center gap-2 border-2 border-cyan-950 w-40 p-2 rounded-lg '
                  }
                  onClick={() => setPath('folders', `/${D}`)}
                >
                  <Usb />
                  <span>{D}</span>
                </div>
              ))}
            {fetch.type !== 'devices' && (
              <>
                <button
                  className='px-5 py-2 text-center border-2 border-cyan-950 w-40 p-2 rounded-lg text-xl'
                  onClick={() => fetchBack()}
                >
                  . /
                </button>
              </>
            )}
            {data.type === 'folders' &&
              (data.folders.length > 0 ? (
                data.folders.map((F) => (
                  <div
                    key={F}
                    className='flex flex-col items-center gap-2 border-2 border-cyan-950 w-40 p-2 rounded-lg'
                    onClick={() => setPath('folders', `/${F}`)}
                  >
                    <Folder />
                    <span>{F}</span>
                  </div>
                ))
              ) : (
                <div>No folders to display</div>
              ))}
            {data.type === 'folders' &&
              (data.files.length > 0 ? (
                data.files.map((F) => (
                  <div
                    key={F}
                    className='flex flex-col items-center gap-2 border-2 border-cyan-950 w-40 p-2 rounded-lg'
                    onClick={() => openModal(F)}
                  >
                    <File />
                    <span>{F}</span>
                  </div>
                ))
              ) : (
                <div>No files to display</div>
              ))}
          </div>
        </>
      )}
      {isModalOpen && (
        <DocumentModal isOpen={isModalOpen} onClose={closeModal} documentUrl={documentURL} />
      )}
      </div>
    </>
  );
};

export default PrintPage;
