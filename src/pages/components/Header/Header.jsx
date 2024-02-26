'use client'

import { Home } from 'lucide-react'
import { useNavigate } from "react-router-dom"

import styles from './Header.module.css'

function Header() {
	const navigate = useNavigate()

 	return (
		<div className={styles.headerContainer} onClick={ ( ) => navigate('/') }>
			<span className={styles.title}>
				<span className={styles.titleBlue}>QAZ </span>PRINT
			</span>
			<button className={styles.homeBtn} onClick={ ( ) => navigate('/') }>
				<Home width={27} height={27}/>
			</button>
		</div>
  	)
}

export default Header
