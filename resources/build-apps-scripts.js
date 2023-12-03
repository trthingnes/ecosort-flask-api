// This file contains the scripts used in SAP Build Apps to fetch from the API


// Image Recognition
const { imagePath, apiUrl } = inputs

const image = await fetch(imagePath)
const blob = await image.blob()
const response = await fetch(apiUrl, {
  method: "POST",
  body: blob,
})
const predictions = await response.json()

return { scores: predictions }


// Create conversation
const { apiUrl } = inputs

const response = await fetch(apiUrl, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: "{}",
})
const chat = await response.json()

return chat


// Create message for picked item in conversation
const { apiUrl, id, chosenItem } = inputs

const response = await fetch(apiUrl + "/" + id, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: `{ "message": "How do I properly dispose of ${chosenItem}?" }`,
})
const chat = await response.json()

return chat


// Create new message in conversation
const { apiUrl, id, message } = inputs

const response = await fetch(apiUrl + "/" + id, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: `{ "message": "${message}" }`,
})
const chat = await response.json()

return chat
