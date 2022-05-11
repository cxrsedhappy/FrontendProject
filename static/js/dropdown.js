let dropdown = document.getElementById("dropdown")
let profileShow = (e) => {
	document.getElementById("dropdown-content").classList.toggle("dropdown-content-show")
}
let profileHide = (e) => {
	if (e.target.id != "dropbtn") {
		if (document.getElementById("dropdown-content").classList.contains("dropdown-content-show")) {
			document.getElementById("dropdown-content").classList.remove("dropdown-content-show")
		}
	}
}

dropdown.addEventListener("click", profileShow)
document.addEventListener("click", profileHide, true)
document.addEventListener("scroll", profileHide, true)
window.addEventListener("resize", profileHide, true)
