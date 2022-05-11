let inputs = []
Array.from(document.getElementsByName("username")).forEach((e) => inputs.push(e))
Array.from(document.getElementsByName("password")).forEach((e) => inputs.push(e))
Array.from(document.getElementsByName("email")).forEach((e) => inputs.push(e))
Array.from(document.getElementsByName("title")).forEach((e) => inputs.push(e))
Array.from(document.getElementsByName("content")).forEach((e) => inputs.push(e))
let labels = []
Array.from(document.getElementsByTagName("label")).forEach((e) => labels.push(e))
labels.map((e, i) => {
	e.addEventListener("click", () => {
		inputs[i].focus()
	})
})
inputs.map((e) => {
	document.addEventListener("click", () => {
		e.removeAttribute("readonly")
	})
	e.addEventListener("focus", () => {
		e.removeAttribute("readonly")
	})
})
