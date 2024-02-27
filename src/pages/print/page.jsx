import axios from "axios"
import { File, Usb } from 'lucide-react'
import { useEffect, useState } from "react"
import Header from "../components/Header/Header"
import styles from './page.module.css'

const PrintPage = () => {
  const [devices, setDevices] = useState([]);
  const [error, setError] = useState(false);

  const fetchData = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/devices");
      if(response.data.status === "error") setError(true);
      else {
        setError(false);
        setDevices(response.data.devices);
      }
    } catch (e) {
      setError(true);
    }
  };

  useEffect(() => {
    setInterval(() => {
    fetchData();
    }, 3000);
  }, []);

  return (
    <>
      <Header />
      <div className={styles.cont}>
        {error ? (
          <div className='flex justify-center flex-col items-center h-screen'>
          <h1>Birdenke durus emes, qaita koriniz</h1>
          <button className='p-2 bg-red-600 text-white rounded' onClick={fetchData}>Reload</button>
          </div>
        ) : (
          <>
            {devices.map(device => (
              <div key={device.deviceName}>
                <div className="flex gap-2 items-center justify-left mb-5 text-3xl">
                  <Usb />
                  <p>{device.deviceName}</p>
                </div>
                
                <div>Files: </div>
                <div className="flex flex-wrap gap-5">
                {device.Path.files.map((file, index) => (
                  <div key={index} className={styles.fileContainer}>
                    <File />
                    <p>{file}</p>
                  </div>
                ))}
                </div>
                <div className='mt-5'>Folders: </div>
                <div className="flex flex-wrap gap-5">
                {device.Path.folders.map((file, index) => (
                  <div key={index} className={styles.fileContainer}>
                    <File />
                    <p>{file}</p>
                  </div>
                ))}
                </div>
              </div>
            ))}
          </>
        )}
      </div>
    </>
  );
};

export default PrintPage;
