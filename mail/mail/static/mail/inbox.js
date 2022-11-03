document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  document.querySelector(".email-list").innerHTML = "";  // clear surface
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  document.querySelector(".email-list").innerHTML = "";  // clear surface

  if (mailbox === "inbox") { 
    // clear up all other component data 
    fetch('/emails/inbox')
      .then(response => response.json())
      .then(emails => {
        // render received emails
        for(const email in emails) { 
          document.querySelector(".email-list").innerHTML += `
            <div class="email-card">
                <div class="email-card-header">
                    <h5 class="email-address">
                        ${emails[email].sender}
                    </h5>
                    <h5 class="email-subject">
                        ${emails[email]["subject"]}
                    </h5>
                </div>
                <p class="email-time">
                    ${emails[email]["timestamp"]}
                </p>
            </div>
          `; 
        }
      });
  }
  else if (mailbox === "sent") { 
    fetch('/emails/sent')
      .then(response => response.json())
      .then(emails => {
        // render received emails
        for(const email in emails) { 
          document.querySelector(".email-list").innerHTML += `
            <div class="email-card">
                <div class="email-card-header">
                    <h5 class="email-address">
                        ${emails[email].recipients[0]}
                    </h5>
                    <h5 class="email-subject">
                        ${emails[email]["subject"]}
                    </h5>
                </div>
                <p class="email-time">
                    ${emails[email]["timestamp"]}
                </p>
            </div>
          `; 
        }
      });
  }
  else if (mailbox === "archive") { 
    fetch('/emails/archive')
      .then(response => response.json())
      .then(emails => {
        // render received emails
        for(const email in emails) { 
          document.querySelector(".email-list").innerHTML += `
            <div class="email-card">
                <div class="email-card-header">
                    <h5 class="email-address">
                        ${emails[email].recipients[0]}
                    </h5>
                    <h5 class="email-subject">
                        ${emails[email]["subject"]}
                    </h5>
                </div>
                <p class="email-time">
                    ${emails[email]["timestamp"]}
                </p>
            </div>
          `; 
        }
      });
  }
}

function send_email() {
  const recepient = document.getElementById("compose-recipients").value;
  // const recepients = recepientStr.split(""); 
  const subject = document.getElementById("compose-subject").value;
  const body = document.getElementById("compose-body").value; 
  // send email 
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recepient,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      load_mailbox("sent"); 
  });
}
