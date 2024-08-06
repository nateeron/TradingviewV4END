
function formatPrice(value, decimals) {
    return Number(value.toFixed(decimals));
}

function removeDuplicates(data) {
    const seen = new Set();
    return data.filter((item) => {
        const duplicate = seen.has(item.time);
        seen.add(item.time);
        return !duplicate;
    });
}

function SortData(data) {
      // Sort the filtered data by time in ascending order
      const sortedData = data.sort((a, b) => a[0] - b[0]);
      return sortedData;
  }

  function StartNewTime(interval, factor) {
      // Define the number of seconds per interval unit
      const intervalUnits = {
          's': 1,            // Seconds
          'm': 60,           // Minutes
          'h': 3600,         // Hours
          'd': 86400,        // Days
          'w': 604800        // Weeks
      };

      // Parse the interval to get the number and the unit
      const intervalValue = parseInt(interval.slice(0, -1), 10);
      const intervalUnit = interval.slice(-1);
      //console.log(intervalValue, intervalUnit, intervalUnits[intervalUnit], factor)
      // Calculate the total number of seconds
      const totalSeconds = intervalValue * intervalUnits[intervalUnit] * factor * 1000;
      //console.log("totalSeconds", totalSeconds)



      return totalSeconds;
  }
  function validateData(data) {
      return data.filter(item => item !== null && item !== undefined);
  }

  function formatPrice(price, decimal) {
      return price.toFixed(decimal);
  }