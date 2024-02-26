import { BrowserRouter, Route, Routes } from 'react-router-dom'
import About from './About'
import './App.css'
import Error from './Error'
import Home from './Home'

export default function App() {
	return (
		<BrowserRouter>
			<Routes>
				<Route>
          <Route path='/' element={<Home />} />
					<Route path='/about' element={<About />} />
					<Route path='/*' element={<Error />} />
				</Route>
			</Routes>
		</BrowserRouter>
	)
}
