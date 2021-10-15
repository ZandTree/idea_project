// dj server expects a sting of tags separated by comma
//  we need to clean and adjust user's input
/*
A. tagsHelp.trimInputTag: cleans tag string
                             1.brings tags to lower case,
                             2.removes comma at the end and 
                             3.trims each tag

B. tagsHelp.converTagsListTo String: takes arr of tags => string
*/
const  tagsHelp ={
    trimInputTag(initialString) {
        // get str input(items separ by ',') and return an cleaned string with items
      let idxLastComma = initialString.lastIndexOf(",");
      // get rid of possible , at the ens of input
      if (initialString.lastIndexOf(",") === initialString.length - 1) {
          initialString = initialString.substr(0, idxLastComma).toLowerCase();
        
      } 
      initialString.toLowerCase();
      let arrFromSplitStr = initialString.split(",");
      let collector = "";
      arrFromSplitStr.forEach((item) => {
        collector += `${item.trim()},`;
      });

      return collector;
    },
    convertTagsListToString(arrTags) {
      //get tag arr and return str where tags separated by ',' 
      let collector = "";
      arrTags.forEach((item) => {
        collector += `${item.trim()},`;
      });
      return collector;
    }
  }
  

  export default tagsHelp