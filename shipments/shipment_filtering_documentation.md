
# Shipment Filtering Documentation

## 1. Filtering by Basic Fields (ForeignKey IDs)

You can filter shipments by these fields which are ForeignKeys to related models.  
Pass the related object's ID in the filter.

| Field            | Description                   |
|------------------|-------------------------------|
| `user`           | Filter by User ID             |
| `driver`         | Filter by Driver ID           |
| `client`         | Filter by Client ID           |
| `client_branch`  | Filter by Client Branch ID    |
| `recipient`      | Filter by Recipient ID        |
| `status`         | Filter by ShipmentStatus ID   |
| `origin_city`    | Filter by Origin City ID      |
| `destination_city`| Filter by Destination City ID|

**Example:**

```
GET /api/shipments/?status=3&origin_city=5
```

This will return shipments with status ID 3 and origin city ID 5.

---

## 2. Date Range Filtering on `loading_date`

Filter shipments loaded within a date range using:

- `loading_date__gte` (Greater Than or Equal to)
- `loading_date__lte` (Less Than or Equal to)

**Example:**

```
GET /api/shipments/?loading_date__gte=2025-06-01&loading_date__lte=2025-06-10
```

Returns shipments loaded between June 1 and June 10, 2025.

---

## 3. Text Search Filtering

Search shipments by:

- `tracking_number`
- `client_invoice_number`

**Example:**

```
GET /api/shipments/?search=INV12345
```

---

## Notes

- Dates should be in `YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SS` format.
- You can combine multiple filters in one request.
- ForeignKey filters require IDs of related objects.
