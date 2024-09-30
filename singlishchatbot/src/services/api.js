import React,{useState} from "react";

const API_URL = process.env.REACT_APP_API_URL || 'http//localhost:8000/api/v1';

export async function sendMessage(userMessage){
    const response = await fetch(`${API_URL}/chat`,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({user_message:userMessage}),
    });
    return response.json();
}

function ChatComponent(){
    
}