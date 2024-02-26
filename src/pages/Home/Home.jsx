import '../../global.css'
import Header from '../components/Header/Header'
import styles from './Home.module.css'

function Home() {
	return (
		<>
			<Header />
			<nav className={styles.navStyle}>
				<div className={styles.navItem}>
					<span className='navItemText'>QYZHAT SHÝGARU</span>
				</div>
				<div className={styles.navItem}>
					<span className='navItemText'>QYZHAT KÒSHÝRU</span>
				</div>
				<div className={styles.navItem}>
					<span className='navItemText'>SCANNERLEU</span>
				</div>
				<div className={styles.navItem}>
					<span className='navItemText'>JARNAMA ORNALASTÝRU</span>
				</div>
			</nav>
		</>
	)
}

export default Home
