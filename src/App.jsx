import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Error from './pages/Error/Error'
import Home from './pages/Home/Home'
import './global.css'

export default function App() {
	return (
		<BrowserRouter>
			<Routes>
				<Route>
					<Route path='/' element={<Home />} />
					<Route path='/home' element={<Home />} />
					<Route path='/*' element={<Error />} />
				</Route>
			</Routes>
		</BrowserRouter>
	)
}
