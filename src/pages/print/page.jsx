import axios from 'axios'
import { File, Folder, Usb } from 'lucide-react'
import { useEffect, useState } from 'react'
import Header from '../components/Header/Header'

const PrintPage = () => {
	const [data, setData] = useState([])
	const [error, setError] = useState(false)
	const [fetch, setFetch] = useState({
		folders: '',
		type: 'devices',
	})

	const fetchData = async () => {
		try {
			const res = await axios.get('http://127.0.0.1:1234/devices')
			if (res.data.status === 'error') setError(true)
			else {
				setError(false)
				setData(res.data)
			}
		} catch (e) {
			setError(true)
		}
	}

	const fetchBack = async () => {
		try {
			const res = await axios.get('http://127.0.0.1:1234/devices/back')
			if (res.data.status === 'error') {
				setError(true)
			} else {
				setError(false)
				setData({ ...res.data, path: res.data.path })
				if (res.data.path === '/Volumes') {
					setFetch({ ...fetch, type: 'devices' })
				}
			}
		} catch (e) {
			setError(true)
		}
	}

	const setPath = async (type, folderName) => {
		setFetch(prev => ({ ...prev, type: type, folders: folderName }))
		if (type === 'folders') {
			try {
				const res = await axios.get(
					`http://127.0.0.1:1234/devices/folder${
						folderName.startsWith('/') ? '' : '/'
					}${folderName}`
				)
				if (res.data.status === 'error') setError(true)
				else {
					setError(false)
					setData(res.data)
				}
			} catch (e) {
				setError(true)
			}
		}
	}

	useEffect(() => {
		fetchData()
	}, [])

	if (error) {
		return <>
			<Header />
      <div className='container mx-auto flex items-center justify-center flex-col'>
				<h1 className='text-2xl text-cyan-950'>USB QÙRYLGUSY TABYLMADY</h1>
				<button className='text-2xl px-4 py-2 bg-red-500 text-white rounded-md' onClick={()=>fetchData()}>JANARTU</button>
			</div>
    </>
	}

	return (
		<>
			<Header />
			<div className='container mx-auto'>
				<h1 className='text-2xl text-cyan-950'>USB QÙRYLGYLARY:</h1>
			</div>
			<div className='container mx-auto flex flex-wrap gap-4 p-5'>
				{data.type === 'devices' && data.devices.length > 0 && data.devices.map(D => (
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
					data.folders.length > 0 &&
					data.folders.map(F => (
						<>
							<div
								key={F}
								className='flex flex-col items-center gap-2 border-2 border-cyan-950 w-40 p-2 rounded-lg'
								onClick={() => setPath('folders', `/${F}`)}
							>
								<Folder />
								<span>{F}</span>
							</div>
						</>
					))}
				{data.type === 'folders' &&
					data.files.length > 0 &&
					data.files.map(F => (
						<>
							<div
								key={F}
								className='flex flex-col items-center gap-2 border-2 border-cyan-950 w-40 p-2 rounded-lg'
							>
								<File />
								<span>{F}</span>
							</div>
						</>
					))}
			</div>
		</>
	)
}

export default PrintPage
