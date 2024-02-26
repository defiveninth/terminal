import { BrowserRouter, Route, Routes } from 'react-router-dom'

import Home from './pages/Home/Home'
import ScanPage from './pages/scan/page'
import PrintPage from './pages/print/page'
import CopyPage from './pages/copy/page'
import Error from './pages/Error/Error'
import AdsPage from './pages/ads/page'

import './global.css'

export default function App() {
	return (
		<BrowserRouter>
			<Routes>
				<Route>
					<Route path='/' element={<Home />} />
					<Route path='/scan' element={<ScanPage />} />
					<Route path='/print' element={<PrintPage />} />
					<Route path='/copy' element={<CopyPage />} />
					<Route path='/ads' element={<AdsPage />} />
					<Route path='/*' element={<Error />} />
				</Route>
			</Routes>
		</BrowserRouter>
	)
}
