export function loadJSON(file) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', `/data/${file}`);
    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(JSON.parse(xhr.response));
      } else {
        const err = new Error(xhr.statusText);
        err.status = xhr.status;
        reject(err);
      }
    };
    xhr.onerror = () => {
      const err = new Error(xhr.statusText);
      err.status = xhr.status;
      reject(err);
    };
    xhr.send();
  });
}
