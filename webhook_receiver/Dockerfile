FROM python:3.7-alpine

ENV PYTHONUNBUFFERED=1
ENV WEBHOOK_PORT=8000
WORKDIR "/tmp/current"
# Note: EXPOSE can't use variables directly, but the actual port binding
# is handled by docker run -p or docker-compose ports section
EXPOSE ${WEBHOOK_PORT}
COPY webhook_receiver.py /

# Use an entrypoint script to handle dynamic port exposure
COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["python3","/webhook_receiver.py"]
