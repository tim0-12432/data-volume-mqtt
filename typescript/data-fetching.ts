
let usedVolumeText: HTMLElement | null = null;
let usedVolumeBar: HTMLElement | null = null;
let usedVolumePercentage: HTMLElement | null = null;
let totalVolumeText: HTMLElement | null = null;
let remainingTimeText: HTMLElement | null = null;
let messageBox: HTMLElement | null = null;

type VolumeData = {
    initialVolume: number,
    initialVolumeStr: string,
    usedVolume: number,
    usedVolumeStr: string,
    remainingSeconds: number,
    remainingTimeStr: string,
}

function addMessage(message: string, type: string) {
    if (messageBox) {
        const messageElement = document.createElement("p");
        messageElement.innerText = message;
        messageElement.classList.add(type);
        messageBox.appendChild(messageElement);
        messageBox.classList.add("show");
    }
}

function removeMessage() {
    if (messageBox) {
        messageBox.innerHTML = "";
        messageBox.classList.remove("show");
    }
}

function fetchData() {
    fetch("/data")
        .then(response => {
            if (response.ok) {
                return response.json()
            } else {
                console.error(response.status + ": " + response.statusText);
                addMessage("Error: " + response.status + ": " + response.statusText, "error");
            }
        })
        .then((data: VolumeData) => {
            removeMessage();
            if (usedVolumeText && usedVolumeBar && totalVolumeText && remainingTimeText && usedVolumePercentage) {
                usedVolumeText.innerText = data.usedVolumeStr;
                usedVolumeBar.style.setProperty("--degree", (data.usedVolume / data.initialVolume * 180).toFixed(0) + "deg");
                usedVolumePercentage.innerText = (data.usedVolume / data.initialVolume * 100).toFixed(1) + "%";
                totalVolumeText.innerText = data.initialVolumeStr;
                remainingTimeText.innerText = data.remainingTimeStr;
            } else {
                console.error("Elements not found! Scripts loaded to early!");
            }
        })
        .catch(error => {
            addMessage("Error fetching volume data!", "error");
            console.error(error);
        });
}

document.addEventListener("DOMContentLoaded", () => {
    usedVolumeText = document.getElementById("used-volume-text");
    usedVolumeBar = document.getElementById("used-volume-bar");
    usedVolumePercentage = document.getElementById("used-volume-percentage");
    totalVolumeText = document.getElementById("total-volume-text");
    remainingTimeText = document.getElementById("remaining-time-text");
    messageBox = document.getElementById("message-box");

    fetchData();
});
