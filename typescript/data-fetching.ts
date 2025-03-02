
let usedVolumeText: HTMLElement | null = null;
let usedVolumeBar: HTMLElement | null = null;
let usedVolumePercentage: HTMLElement | null = null;
let remainingDataBar: HTMLElement | null = null;
let totalVolumeText: HTMLElement | null = null;
let remainingTimeText: HTMLElement | null = null;
let remainingTimeBar: HTMLElement | null = null;
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


function getPercentageOfDaysRemaining(remainingSeconds: number): number {
    const today = new Date();
    const daysOfCurrMonth = new Date(today.getFullYear(), today.getMonth() + 1, 0).getDate();
    const secondsOfCurrMonth = daysOfCurrMonth * 24 * 60 * 60;
    return (secondsOfCurrMonth - remainingSeconds) / secondsOfCurrMonth * 100;
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
            if (usedVolumeText && usedVolumeBar && totalVolumeText && remainingDataBar && remainingTimeText && usedVolumePercentage && remainingTimeBar) {
                usedVolumeText.innerText = data.usedVolumeStr;
                usedVolumeBar.style.setProperty("--degree", (data.usedVolume / data.initialVolume * 180).toFixed(0) + "deg");
                const percentageVolume = (data.usedVolume / data.initialVolume * 100).toFixed(0) + "%";
                usedVolumePercentage.innerText = (data.usedVolume / data.initialVolume * 100).toFixed(1) + "%";
                remainingDataBar.style.setProperty("--percentage", percentageVolume);
                remainingDataBar.getElementsByTagName("p").item(0)!.innerText = percentageVolume;
                totalVolumeText.innerText = data.initialVolumeStr;
                remainingTimeText.innerText = data.remainingTimeStr;
                const percentageTime = getPercentageOfDaysRemaining(data.remainingSeconds).toFixed(0) + "%"
                remainingTimeBar.style.setProperty("--percentage", percentageTime);
                remainingTimeBar.getElementsByTagName("p").item(0)!.innerText = percentageTime;
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
    remainingDataBar = document.getElementById("remaining-data-bar");
    totalVolumeText = document.getElementById("total-volume-text");
    remainingTimeText = document.getElementById("remaining-time-text");
    remainingTimeBar = document.getElementById("remaining-time-bar");
    messageBox = document.getElementById("message-box");

    fetchData();
});
