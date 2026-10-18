import React from 'react'
import { Login } from '../../components/Login/Login'
import { Logout } from '../../components/Logout/Logout'

export const LoginPage = () => {
  return (
    <div>
        <p>Wlecome User</p>
        <Login />
        <Logout/>
        
    </div>
  )
}
