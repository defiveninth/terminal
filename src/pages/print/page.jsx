'use client'

import axios from "axios"
import { useState } from "react"
import { Usb, File } from 'lucide-react';

import Header from "../components/Header/Header"

import styles from './page.module.css'

 let reqOptions = {
  url: "https://localhost:5000",
  method: "GET",
  headers: {
    "Accept": "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.com)"
   }
 }

const PrintPage = async () => {
  const [error, setError] = useState<Boolean>(false)

  try {
    let response = await axios.request(reqOptions)
  } catch (e) {
    setError(true)
  }

  return (
    <>
        <Header />
        <div className={ styles.cont }>
          {
            error ? (
              <>
                <h1>Birdenke durus emes, qaita koriniz</h1>
                <button></button>
              </>
            ) : (
              <>
                {
                  response.data.devices.map(D => (<>
                    <div key={D.deviceName}>
                      <Usb />
                      <p>{ D.deviceName }</p>
                      <div>files: </div>
                        {
                          response.data.devices.files.map(F => <div key={ F }>
                            <File />
                            <p>{ F }</p>
                          </div>)
                        }
                    </div>
                  </>))
                }
              </>
            )
          }
        </div>
    </>
  )
}

export default PrintPage
