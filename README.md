# kitchen assistant
- Kitchen assistant is an AI device, which makes your kitchen interactive

## Purpose
- To prove the concept that kitchen assistant encourage visually impaired people to cook new dishes

## Goal
- I can cook stir-fry without visual input in the condition where the ingredients are cut in advance

## Why
- Chances that visually impaired people cook new dishes at home are very limited because the ways to share recipes rely on visual input too much

## How
1. Replace the existing ways to share recipes with voice interface
2. Assist the decision by visual inputs with computer vision

## Details
1. Replace the existing ways to share recipes with voice interface -> TBC
2. Assist the decision by visual inputs with computer vision -> TBC

## Constraints
- Limit recipe to stir-fry
- Focus more on cooking than organizing the cooking area or detecting ingredients

## Risk
- Voice detection doesn't work well during cooking, especially frying

## Development env
- Install `ngrok`
```
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok
```
```
ngrok http 8000
```
