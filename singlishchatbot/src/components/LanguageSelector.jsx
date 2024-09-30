import React from 'react';

const LanguageSelector = ({currentLanguage,onlanguagechange})=>{
    return (
        <select value={currentLanguage} onChange={(e) => onlanguagechange(e.target.value)} >
            <option value="sn">Singlish</option>
            <option value="en">English</option>
            <option value="ta">Tamil</option>
            <option value="si">Sinhala</option>
        </select>
    )
}
export default LanguageSelector;