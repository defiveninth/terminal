import styles from './Header.module.css'
import { Home } from 'lucide-react';
function Header() {
  return (
	<div className={styles.headerContainer}>
		<span className={styles.title}>
			<span className={styles.titleBlue}>QAZ </span>PRINT
		</span>

		<button className={styles.homeBtn}><Home width={27} height={27}/></button>
	</div>
  )
}

export default Header
