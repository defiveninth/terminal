'use client'

import { useNavigate } from "react-router-dom"

import Header from '../components/Header/Header'

import '../../global.css'
import styles from './Home.module.css'

const Home = () => {
	const navigate = useNavigate()
	return (
		<div className='flex flex-col mt-20'>
			<Header />
			<nav className={styles.navStyle}>
				<div className={styles.navItem} onClick={ () => navigate('/print') }>
					<span className='navItemText'>QYZHAT SHÝGARU</span>
				</div>
				<div className={styles.navItem} onClick={ () => navigate('copy') }>
					<span className='navItemText'>QYZHAT KÒSHÝRU</span>
				</div>
				<div className={styles.navItem} onClick={ () => navigate('scan') }>
					<span className='navItemText'>SCANNERLEU</span>
				</div>
				<div className={styles.navItem} onClick={ () => navigate('/ads') }>
					<span className='navItemText'>JARNAMA ORNALASTÝRU</span>
				</div>
			</nav>
		</div>
	)
}

export default Home
