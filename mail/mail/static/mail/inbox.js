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
          console.log(emails[email].read);
          document.querySelector(".email-list").innerHTML += `
            <div class="email-card" onclick="load_full_email(${emails[email].id})">
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
            <div class="email-card" onclick="load_full_email(${emails[email].id})" >
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
            <div class="email-card" onclick="load_full_email(${emails[email].id})" >
                <div class="email-card-header">
                    <h5 class="email-address">
                        ${emails[email].recipient[0]}
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
  const recepients = document.getElementById("compose-recipients").value;
  // const recepients = recepientStr.split(","); 
  const subject = document.getElementById("compose-subject").value;
  const body = document.getElementById("compose-body").value; 
  // send email 
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recepients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      load_mailbox("sent"); 
  })
}

function load_full_email(target) { 
  document.querySelector('#emails-view').style.display = "none";
  // update viewing
  fetch(`/emails/${target}`, {
    method: 'PUT',
    body: JSON.stringify({
        viewed: true
    })
  })

  // fetch corresponding data from api 
  fetch(`/emails/${target}`)
    .then(response => response.json())
    .then(email => {
      console.log(email.recipients)
      // render the component
      document.querySelector(".email-list").innerHTML = `
        <div class="email-full-data">
            <hr />
            <p>
                <span style="font-weight: bolder">From: </span>   
                ${email.sender}
            </p>  
            <p>
                <span style="font-weight: bolder">To: </span>   
                ${email.recipients}
            </p>  
            <p>
                <span style="font-weight: bolder">Subject: </span>   
                ${email.subject}
            </p>  
            <p>
                <span style="font-weight: bolder">Timestamp: </span>   
                ${email.timestamp}
            </p>  
            <div class="email-view-btns">
                <button class="btn btn-sm btn-outline-dark" id="reply-btn" onclick="handleReplying('${email.sender}', '${email.subject}', '${email.timestamp}', '${email.body}')">Reply</button>
                <button class="btn btn-sm btn-outline-dark" id="archive-btn" onclick="toggleArchive(${email.id}, ${email.archived})"> ${ (email.archived)?"Unarchive":"Archive"} </button>
            </div>
            <hr />
            <h6>
              ${email.body}
            </h6>
        </div>
      `; 
    });
}

function handleReplying(sender_email, subject, timestamp, body) { 
  compose_email(); 
  // set the value of recipient 
  document.getElementById("compose-recipients").value = sender_email; 
  // set the value for subject 
  document.getElementById("compose-subject").value = `Re: ${subject}`;
  // set the initial body text
  document.getElementById("compose-body").value = `On ${timestamp} ${sender_email} wrote: 
    ${body} 
  `;
}

function toggleArchive(target, status) {
  if (!status) {
    fetch(`/emails/${target}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: true
      })
    }).then (()  => {
        load_mailbox("archive"); 
      }
    )
  } 
  else { 
    fetch(`/emails/${target}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: false
      })
    }).then (()  => {
        load_mailbox("inbox"); 
      }
    )
  }
}