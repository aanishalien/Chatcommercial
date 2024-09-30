import React from 'react';

const ChatWindow = ({messages}) =>{
    return(
        <div className="chat-wndow">
            {messages.map((message,index)=>{
                <div key={index} className={`message ${message.sender}`}>
                    {message.text}
                    <p className="warning">Do not share personal or bank account details.</p>
                </div>
            })}
        </div>
    )
}

export default ChatWindow