# PoC for boundary support in FU-A

PoC for algorithm to parse weird boundaries in FU-A packets in an RTSP stream.

Original project for which this PoC is made: [retina](https://github.com/scottlamb/retina)

Cases for PoC and status outlined below.

## Progress

- [x] Single pkt
    - [x] boundary at start
    - [x] boundary in middle
- [ ] Multiple pkts
    - [x] boundary across pkts only
    - [ ] boundary across pkts AND in middle of same pkt

## Single packet

### Boundary in middle

#### Input

```
[A - boundary - B]
```

#### Output

```
[ [A], [B] ]
```

### Boundary at start

#### Input

```
[boundary - A]
```

#### Output

```
[ [A] ]
```

### Boundary at end

Not possible for a single pkt, as boundary at the end could mean that the
boundary is either extended to next pkt, or that the boundary ends at the end
of this pkt.

However, we won't know until we start reading the next pkt, hence
this case will be covered by multiple pkt flow.

## Multiple packet

### Boundary across pkts only

#### Input

```
[ [A], [B - boundary], [boundary - C] ]
```

#### Output

```
[ [A], [B], [C] ]
```

### Boundary across pkts and in middle too

#### Input

```
[ [A], [B - boundary], [boundary - C - boundary - D] ]
```

#### Output

```
[ [A], [B], [C], [D] ]
```
