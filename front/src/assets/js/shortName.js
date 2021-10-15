const getFileNameFromUrl = (urlName)=>{
    const arr= urlName.split('\/')
    return arr[arr.length-1]
    
        
}
export default getFileNameFromUrl