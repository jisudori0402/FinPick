import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

export const clearAuthStorage = () => {
  localStorage.removeItem('isLoggedIn')
  localStorage.removeItem('username')
  localStorage.removeItem('email')
  localStorage.removeItem('name')
  localStorage.removeItem('latestDiagnosisResult')
}

const saveAuthUser = (user) => {
  localStorage.setItem('isLoggedIn', 'true')
  localStorage.setItem('username', user?.username || '')
  localStorage.setItem('email', user?.email || '')
  localStorage.setItem('name', user?.name || '')
}

const syncLatestDiagnosisResult = async () => {
  const response = await axios.get(`${API_BASE_URL}/api/diagnosis/latest/`, {
    withCredentials: true,
  })

  if (response.data.result) {
    localStorage.setItem('latestDiagnosisResult', JSON.stringify(response.data.result))
    return
  }

  localStorage.removeItem('latestDiagnosisResult')
}

export const notifyAuthChanged = () => {
  window.dispatchEvent(new Event('auth-state-changed'))
}

export const syncAuthFromSession = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/session/`, {
      withCredentials: true,
    })

    if (response.data.authenticated) {
      saveAuthUser(response.data.user)
      await syncLatestDiagnosisResult()
      return true
    }
  } catch (err) {
    console.error(err)
  }

  clearAuthStorage()
  return false
}

export const logoutSession = async () => {
  try {
    await axios.post(
      `${API_BASE_URL}/api/logout/`,
      {},
      {
        withCredentials: true,
      },
    )
  } finally {
    clearAuthStorage()
    notifyAuthChanged()
  }
}
