import { DeviceDiscoveryInformation } from '#components/form-sections';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('DeviceDiscoveryInformation', () => {
  let component: DeviceDiscoveryInformation;
  let fixture: ComponentFixture<DeviceDiscoveryInformation>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DeviceDiscoveryInformation],
    }).compileComponents();

    fixture = TestBed.createComponent(DeviceDiscoveryInformation);
    component = fixture.componentInstance;

    // Set required input
    component.mac = {
      id: 1,
      address: '00:11:22:33:44:55',
      last_ip: '192.168.1.100',
      hostname: 'test-host',
      last_seen: '2024-01-01T00:00:00Z',
      device: null,
      discoveries: [],
      ports: [],
    };

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
