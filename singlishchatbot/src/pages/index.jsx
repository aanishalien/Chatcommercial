import { useState,useEffect } from "react";
import Head from "next/head";
import Image from "next/image";
import { Inter } from 'next/font/google'
import combank from '@/Images/combank.png'
import styles from '@/styles/Home.module.css'
import axios from 'axios';
import LanguageSelector from "@/components/LanguageSelector";
import ChatWindow from "@/components/ChatWindow";

const inter = Inter({ subsets: ['latin'] });

export default function Home() {
  const [inputValue, setInputValue] = useState('');
  const [chatLog, setChatLog] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedIssue,setSelectedIssue]=useState('transfer');
  const [currentLanguage,setCurrentLanguage] = useState('en');

  const handleLanguageChange = (newLanguage)=>{
    setCurrentLanguage(newLanguage);
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    setChatLog((prevChatLog) => [...prevChatLog, { type: 'user', message: `${selectedIssue}: ${inputValue}` }]);
    sendMessage(inputValue);
    setInputValue('');

  }

  const sendMessage = async(message)=>{
    const isRelated = checkMessageValidity(message,selectedIssue);

    if(!isRelated){
      setChatLog((prevChatLog)=>[
        ...prevChatLog,
        {type:'bot',message:"This is not the issue that you selected."}
      ]);
      return;
    }
    try{
      const response = await axios.post('http://localhost:8000/api/v1/chat',{
        user_message: inputValue
      });
      console.log(response.data);
      setChatLog((prevChatLog)=>[...prevChatLog,{type:'bot',message:response.data.response}]);
    } catch(error){
      console.error("Error:",error);
    }
  }
  //check if the message is related to the selected issue

  const checkMessageValidity =(message,issueType)=>{
    const keywords = {
      transfer:["transfer","send money","funds"],
      bank_account:["account","balance","bank","statement"],
      general_question:["question","help","support"]
    };

    const issueKeywords = keywords[issueType] ||[];
    return issueKeywords.some(keywords => message.toLowerCase().includes(keywords));
  };

  return (
    <div className="container mx-auto max-w-[700px] px-4">
      <div className="flex flex-col h-screen bg-gray-900">
        <div className="flex justify-center mt-4">
          <Image
            src={combank}
            alt="Chatbot-Image"
            width={150}
            height={150}
            className="rounded-full"
          />
        </div>
        <div className="flex justify-center mt-4">
          <LanguageSelector currentLanguage={currentLanguage} onlanguagechange={handleLanguageChange}/>
        </div>

        <div className="flex-grow p-6">
          <ChatWindow messages={chatLog}/>
        </div>
        
        <div className="flex-grow p-6">
          <div className="flex flex-col space-y-4">
          {
          chatLog.map((message, index) => (
            <div key={index} className={`flex ${
              message.type === 'user' ? 'justify-end' :'justify-start'
            }`}>
              <div className={` ${
                message.type === 'user' ? 'bg-purple-500' : 'bg-gray-800'
              } rounded-lg p-4 text-white max-w-sm` }>
                {message.message}
              </div>
              </div>
          ))
          }
          </div>
        </div>
      
      <form onSubmit={handleSubmit}>
          <div className="flex flex-col mb-4">
            <label htmlFor="text-white mb-2">Select Issue Type:</label>
            <select 
              className="p-2 rounded-lg bg-gray-800 text-white border border-gray-700"
              value={selectedIssue}
              onChange={(e) => setSelectedIssue(e.target.value)}
              >
                <option value="transfer">Transfer Issue</option>
                <option value="bank_account">Bank Account Issue</option>
                <option value="general_question">General Question</option>
              </select>
          </div>
        <div className="flex rounded-lg border border-gray-700 bg-gray-800">
          <input type="text" className="flex-grow px-4 py-2 bg-transparent text-white focus:outline-none" placeholder="Type your message..." value={inputValue} onChange={(e) => setInputValue(e.target.value)} />
          <button className="bg-purple-500 rounded-lg px-4 py-2 font-semibold focus:outline-none hover:bg-purple-600 transition-colors duration-300" type="submit">Send</button>
        </div>
      </form>
      </div>
    </div>
  );
}