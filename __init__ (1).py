<h2>AI Room Suggestion</h2>

{% if room %}
<p>Suggested Room: {{ room.room_number }}</p>
{% else %}
<p>No rooms available.</p>
{% endif %}