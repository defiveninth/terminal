import Header from '../components/Header/Header'
import styles from './page.module.css'

const AdsPage = () => {
	return (
		<>
			<div className={styles.wrapper}>
				<Header />
				<form action='' method='post' className={styles.adsForm}>
          <h2 className={styles.titleForm}>| JARNAMA ORNALASTYRU</h2>
					<input type='text' name='' id='' className={styles.formInput} placeholder='ESIMIŃIZ'/>
					<input type='text' name='' id='' className={styles.formInput} placeholder='EMAIL'/>
					<button type='submit' className={styles.formBtn}>Jiberu</button>
				</form>
			</div>
		</>
	)
}

export default AdsPage
