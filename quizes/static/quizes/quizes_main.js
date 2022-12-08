console.log("Hello! Quizes_main")

const modalBtns = [...document.getElementsByClassName('modal-button')]
const modalBody = document.getElementById('modal-body-confirm')
const startBtn = document.getElementById('start-button')

const url = window.location.href
console.log(url)

modalBtns.forEach(modalBtn=>modalBtn.addEventListener('click', ()=>{
	const pk = modalBtn.getAttribute('data-pk')
	const name = modalBtn.getAttribute('data-quiz')
	const numQuestions = modalBtn.getAttribute('data-questions')
	const difficulty = modalBtn.getAttribute('data-difficulty')
	const scoreToPass = modalBtn.getAttribute('data-pass')
	const time = modalBtn.getAttribute('data-time')
	const classId = modalBtn.getAttribute('data-class_id')

	modalBody.innerHTML = `
		<div class="h5 mb-3">Are you sure you want to Start <b>${name}</b> ?</div>
		<div class="text-muted">
			<ul>
				<li>Difficulty : <b>${difficulty}</b></li>
				<li>Questions : <b>${numQuestions}</b></li>
				<li>Passing Score : <b>${scoreToPass} %</b></li>
				<li>Duration : <b>${time} min</b></li>
			</ul>
		</div>
	`
	console.log(pk)
	startBtn.addEventListener('click', () => {
		window.location.href = url + pk 

	})
	
}))