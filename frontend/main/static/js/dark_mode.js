function darkmode() {
	var SetTheme = document.body;

	SetTheme.classList.toggle("dark");
	
	var theme;

	if (SetTheme.classList.contains("dark")) {
		console.log("dark");
		theme = "dark";
	} else {
		console.log("light");
		theme = "light";
	}

	localStorage.setItem("PageTheme", JSON.stringify(theme));
}

let GetTheme = JSON.parse(localStorage.getItem("PageTheme"));
console.log(GetTheme);

if (GetTheme == "dark") {
	document.body.classList = "dark";
}