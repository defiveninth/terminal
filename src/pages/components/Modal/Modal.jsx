import {
  faArrowLeft,
  faArrowRight,
  faPrint,
  faTimes,
} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import React from 'react'
import Modal from 'react-modal'
import { Document, Page, pdfjs } from 'react-pdf'
import styles from './Modal.module.css'; // Import your CSS file for styling

Modal.setAppElement('#root')

const DocumentModal = ({ isOpen, onClose, documentUrl }) => {
	const [numPages, setNumPages] = React.useState(null)
	const [pageNumber, setPageNumber] = React.useState(1)
	const [error, setError] = React.useState(null)
	const [pageRange, setPageRange] = React.useState({ start: 1, end: 1 })

	pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`

	const handleLoadSuccess = ({ numPages }) => {
		setNumPages(numPages)
		setPageRange({ start: 1, end: numPages })
	}

	const handleLoadError = error => {
		setError(error)
	}

	const handlePrevPages = () => {
    const newStart = Math.max(pageRange.start - numPages, 1);
    setPageRange({ start: newStart, end: newStart + numPages - 1 });
  };

  const handleNextPages = () => {
    const newStart = Math.min(pageRange.start + numPages, numPages);
    setPageRange({ start: newStart, end: newStart + numPages - 1 });
  };

  const handlePrint = () => {
    window.print();
  };

	return (
		<Modal
			isOpen={isOpen}
			onRequestClose={onClose}
			className={styles.modalContent}
		>
			<button onClick={onClose} className={styles.closeModal}>
				✕
			</button>
			{error ? (
				<div>Error loading PDF: {error.message}</div>
			) : (
				<div className={styles.pdfContainer}>
					<div className={styles.pdfWrapper}>
						<Document
							file={documentUrl}
							onLoadSuccess={handleLoadSuccess}
							onLoadError={handleLoadError}
						>
							{Array.from(
								new Array(pageRange.end - pageRange.start + 1),
								(el, index) => (
									<Page
										key={index + pageRange.start}
										pageNumber={index + pageRange.start}
										className={styles.pdfPage}
									/>
								)
							)}
						</Document>
					</div>
				</div>
			)}
			<p>
				Pages {pageRange.start} - {pageRange.end} of {numPages}
			</p>
			<div className={styles.btnList}>
      <button onClick={handlePrint}>
        <FontAwesomeIcon icon={faPrint} className={styles.icon} />
      </button>
			</div>
		</Modal>
	)
}

export default DocumentModal
