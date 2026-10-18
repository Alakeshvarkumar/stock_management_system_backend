import { useState } from 'react'
import { Home } from './Pages/Home/Home'
import { Navbar } from './components/Navbar/Navbar'
import { LoginPage } from './Pages/Login/LoginPage'
import { Routes, Route,Navigate } from 'react-router-dom'
import './App.css'

function App() {
  

  return (
    <div>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path='/nav' element={<Navbar/>} />
        <Route path='/login' element ={<LoginPage/>}/>
      </Routes>
    </div>
  )
}

export default App
