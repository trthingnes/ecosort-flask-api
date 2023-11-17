// This script can be used in SAP Build Apps to fetch from this API
// The inputs object is defined using the variables next to the JS code block in Build Apps
const { imagePath, apiUrl } = inputs

const image = await fetch(imagePath)
const blob = await image.blob()
const response = await fetch(apiUrl, {
  method: "POST",
  body: blob,
})
const predictions = await response.json()

return { scores: predictions }
